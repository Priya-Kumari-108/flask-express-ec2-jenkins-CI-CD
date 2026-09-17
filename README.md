# Jenkins CI/CD Pipeline Assignment

# Part 1 – Manual Deployment of Flask Backend and Express Frontend on AWS EC2

---

## 1. Introduction

This project is part of a DevOps and Jenkins CI/CD assignment.

The purpose of Part 1 was to understand the fundamentals of deploying applications on a cloud server before automating the deployment using Jenkins.

In this part, I deployed two applications:

1. A Flask backend application written in Python.
2. An Express frontend/server application written in Node.js.

Both applications were deployed on the same AWS EC2 instance.

The Flask backend was configured to run on port `5000`, while the Express frontend was configured to run on port `3000`.

After getting both applications running manually, I configured process managers so that the applications could continue running in the background and automatically start again after the EC2 server was restarted.

For the Flask backend, I used:

systemd

For the Express frontend, I used:

PM2

The main architecture of Part 1 was:


                    Internet
                       |
                       |
                AWS EC2 Instance
              Ubuntu Linux Server
                       |
              +--------+--------+
              |                 |
              |                 |
        Flask Backend      Express Frontend
          Port 5000           Port 3000
              |                 |
           systemd              PM2
              |                 |
              +--------+--------+
                       |
                  Application
                    Server






                    
Repository structure:
flask-express-ec2-jenkins-CI-CD/
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
└── frontend/
    ├── server.js
    ├── package.json
    └── package-lock.json



    
Technology Stack

| Layer                    | Technology                 |
| ------------------------ | -------------------------- |
| Cloud                    | AWS                        |
| Compute                  | Amazon EC2                 |
| Operating System         | Ubuntu                     |
| Backend Language         | Python                     |
| Backend Framework        | Flask                      |
| Frontend/Server          | Node.js                    |
| Frontend Framework       | Express                    |
| Source Control           | Git                        |
| Repository               | GitHub                     |
| Python Environment       | Python Virtual Environment |
| Backend Process Manager  | systemd                    |
| Frontend Process Manager | PM2                        |
| Backend Port             | 5000                       |
| Frontend Port            | 3000                       |



    
What is systemd?

systemd is the service management system used by modern Linux distributions.

It can:

Start applications.
Stop applications.
Restart applications.
Monitor services.
Start services during boot.
Check service status.


Creating the Flask systemd Service

sudo nano /etc/systemd/system/backend.service

The service configuration was:

[Unit]
Description=Flask Backend Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/flask-express-ec2-jenkins-CI-CD/backend
ExecStart=/home/ubuntu/flask-express-ec2-jenkins-CI-CD/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target


Command i have used:
Reloading systemd: sudo systemctl daemon-reload

Starting the Backend Service: sudo systemctl start backend
The status was checked using: sudo systemctl status backend
Enabling the Backend at Boot:
  sudo systemctl start backend
  sudo systemctl enable backend

What is PM2?

PM2 is a process manager for Node.js applications.

It can:

Start Node.js applications.
Keep applications running in the background.
Restart applications.
Monitor processes.
Show application status.
Restore applications after a server reboot.

The architecture becomes:
EC2
 |
 v
PM2
 |
 v
Express
 |
 v
Port 3000


Starting Express with PM2:
pm2 start server.js --name frontend

Checking PM2 Status:
pm2 status

Saving the PM2 Process List:
pm2 save

Configuring PM2 Startup:
pm2 startup



Complete Deployment Flow

1. Create EC2 instance
          |
          v
2. Configure Security Group
          |
          v
3. Connect to Ubuntu server
          |
          v
4. Install Git, Python and Node.js
          |
          v
5. Clone GitHub repository
          |
          +-----------------------+
          |                       |
          v                       v
     BACKEND                  FRONTEND
          |                       |
          v                       v
Create Python venv          npm install
          |                       |
          v                       v
Install Flask              Start Express
dependencies                    |
          |                       v
          v                      PM2
Start Flask                     |
          |                       v
          v                  Port 3000
       systemd
          |
          v
      Port 5000




