from flask import Flask, render_template, request
import socket
import threading

app = Flask(__name__)

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "Remote Desktop",
    8080: "HTTP Alternate"
}

results = []


def scan_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        connection = s.connect_ex((host, port))

        if connection == 0:
            results.append({
                "port": port,
                "service": COMMON_PORTS[port],
                "status": "Open"
            })

        s.close()

    except:
        pass


@app.route("/", methods=["GET", "POST"])
def home():
    global results
    results = []

    if request.method == "POST":

        host = request.form["host"]

        try:
            ip = socket.gethostbyname(host)

            threads = []

            for port in COMMON_PORTS:

                thread = threading.Thread(
                    target=scan_port,
                    args=(ip, port)
                )

                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            return render_template(
                "index.html",
                host=host,
                ip=ip,
                results=results,
                total=len(results)
            )

        except Exception as e:

            return render_template(
                "index.html",
                error=str(e)
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)