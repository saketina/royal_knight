FROM python:3.11.2

COPY requirements.txt .
RUN pip install -r requirements.txt

# RUN ln -sv /dev/stdout /home/admin/logs/server.log
# RUN ln -sv /dev/stderr /home/admin/logs/server-errors.log

COPY . .

CMD ["python", "main.py"]
# CMD ["docker", "logs", "-f", "royal_knight", ">", "/home/admin/logs/client.txt"]
