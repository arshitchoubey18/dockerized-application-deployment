# 🚀 Dockerized Application Deployment

This project demonstrates how to containerize a Python Flask application using Docker and run it using both Docker and Docker Compose.

---

## 📌 Project Overview

- Built a simple Flask web application  
- Containerized the application using Docker  
- Managed Docker images and containers  
- Used Docker Compose for simplified deployment  
- Demonstrated container lifecycle and networking  

---

## 🛠️ Tech Stack

- Python (Flask)  
- Docker  
- Docker Compose  

---

## 📁 Project Structure

```bash
dockerized-application-deployment/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore

```

⚙️ Prerequisites

Ensure the following are installed on your system:

```
Docker
Docker Compose
Git
```
Verify Installation
```
docker --version
docker compose version
git --version
```

📥 Clone the Repository
```
git clone https://github.com/arshitchoubey18/dockerized-application-deployment.git
cd dockerized-application-deployment
```
▶️ Run the Project using Docker
```
Step 1: Build Docker Image
docker build -t dockerized-flask-app:v1 .

Step 2: Run Docker Container
docker run -d -p 5000:5000 --name flask-container dockerized-flask-app:v1

Step 3: Access the Application

Application: http://localhost:5000
Health Check: http://localhost:5000/health
```

▶️ Run the Project using Docker Compose (Recommended)
```
Step 1: Build and Start Services
docker compose up -d --build
Step 2: Access the Application

http://localhost:5000
```
🔄 Container Management
```
docker ps
docker logs flask-container
docker stop flask-container
docker rm flask-container
```
🔄 Docker Compose Commands
```
docker compose logs
docker compose down
```
🌐 Networking Explanation
```
Port mapping:

5000:5000
First 5000 → Host machine port
Second 5000 → Container port

Access the application via:

http://localhost:5000
```
🧪 Versioning Example
```
docker build -t dockerized-flask-app:v2 .
docker run -d -p 5000:5000 dockerized-flask-app:v2
```
❗ Troubleshooting
```
Port already in use
sudo lsof -i :5000

OR run on a different port:

docker run -d -p 8080:5000 dockerized-flask-app:v1

Then access:

http://localhost:8080

📸 Output

Add screenshots here (optional)
```
📚 Learning Outcomes
```
Dockerfile creation
Image building and tagging
Container lifecycle management
Docker Compose usage
Networking and port mapping
```

🎯 Why This Project?
```
This project demonstrates real-world DevOps practices such as:

Application containerization
Environment consistency
Reproducible deployments
🤝 Contributing
```
Feel free to fork and improve this project.

👤 Author

Arshit Choubey
