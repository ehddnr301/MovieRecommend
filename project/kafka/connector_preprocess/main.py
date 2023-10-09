import subprocess
import json
import os


def post_connector(json_file):
    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "http://connect-service:8083/connectors",
            "-H",
            "Content-Type: application/json",
            "-d",
            f"@{json_file}",
        ]
    )


def main():
    # 현재 디렉토리의 모든 파일을 나열합니다.
    for filename in os.listdir("."):
        # .json 확장자를 가진 파일만 처리합니다.
        if filename.endswith(".json"):
            post_connector(filename)


if __name__ == "__main__":
    main()
