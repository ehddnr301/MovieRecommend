import subprocess
import json


def main():
    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "http://connect-service:8083/connectors",
            "-H",
            "Content-Type: application/json",
            "-d",
            "@source_connector.json",
        ]
    )

    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "http://connect-service:8083/connectors",
            "-H",
            "Content-Type: application/json",
            "-d",
            "@sink_connector.json",
        ]
    )


if __name__ == "__main__":
    main()
