import json
import os
import subprocess
import sys
import urllib.request

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)


def get_git_diff():
    try:
        subprocess.run(
            ["git", "rev-parse"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print(
            "Error: Not a git repository. Please run this script in a git repository."
        )
        sys.exit(1)

    try:
        return subprocess.check_output(["git", "diff", "--staged"]).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        sys.exit(1)


def generate_commit_message(diff) -> str:
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}",
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Write commit message for the change with commitizen convention. Keep the title under 50 characters and wrap message at 72 characters. Format as a gitcommit code block. Only reply commit message",
                },
                {"role": "user", "content": f"Here are the changes:\n\n{diff}"},
            ],
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode("utf-8"))
        message = response_data["choices"][0]["message"]["content"]
        if not message:
            return ""

        message = message.strip()
        message = message.replace("```gitcommit", "").replace("```", "").strip()

        return message
    except Exception as e:
        print(f"Error generating commit message: {e}")
        sys.exit(1)


def commit_and_push(commit_message):
    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        print(commit_message)

        push = input("Push changes to remote? (y/n): ").lower()
        if push == "y":
            subprocess.run(["git", "push"], check=True)
            print("Changes pushed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error in git operations: {e}")
        sys.exit(1)


def main():
    diff = get_git_diff()
    if not diff:
        print("No staged changes found. Use 'git add' to stage changes.")
        sys.exit(0)

    commit_message = generate_commit_message(diff)
    commit_and_push(commit_message)


if __name__ == "__main__":
    main()
