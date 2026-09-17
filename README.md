# Jenkins CI/CD Pipeline Assignment   {https://github.com/Priya-Kumari-108/flask-express-ec2-jenkins-CI-CD}

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







 Part 2 — Implementing CI/CD Using Jenkins

 1. Introduction

In Part 1, I manually deployed the Flask backend and Express frontend on an AWS EC2 instance.

The applications were running successfully, but whenever I made changes to the source code, I still needed to manually:

1. Pull the latest code from GitHub.
2. Install/update dependencies if required.
3. Restart the application.
4. Check whether the application was running correctly.

This process is repetitive and can lead to mistakes.

Therefore, in Part 2, I implemented a CI/CD pipeline using Jenkins.

The goal was to automate the deployment process so that whenever new code is pushed to the GitHub repository, GitHub sends a webhook notification to Jenkins and Jenkins automatically starts the required pipeline.

---

2. Objective of Part 2

The main objectives of Part 2 were:

- Install and configure Jenkins.
- Connect Jenkins with GitHub.
- Create separate Jenkins pipelines for:
  - Flask Backend
  - Express Frontend
- Automatically obtain the latest source code from GitHub.
- Deploy the backend using systemd.
- Deploy the frontend using PM2.
- Configure GitHub Webhooks.
- Automatically trigger Jenkins pipelines when code is pushed.
- Perform health checks after deployment.
- Verify that both applications are running successfully.

---

 3. Technology Stack

| Technology | Purpose |
|------------|---------|
| AWS EC2 | Server for applications and Jenkins |
| Ubuntu | Operating system |
| Jenkins | CI/CD automation server |
| GitHub | Source code management |
| Git | Version control |
| Python | Backend programming language |
| Flask | Backend framework |
| Node.js | JavaScript runtime |
| Express | Frontend/server application |
| systemd | Flask process management |
| PM2 | Express process management |
| Bash | Deployment automation |
| rsync | Synchronizing application files |
| curl | Health checking |
| GitHub Webhook | Automatically notifying Jenkins |

---

 4. Part 2 Architecture

The final CI/CD architecture is:

```text
                    Developer
                        |
                        | git push
                        ↓
                    GitHub
                        |
                        | GitHub Webhook
                        ↓
                  Jenkins Server
                        |
              ┌─────────┴─────────┐
              ↓                   ↓
       Backend Pipeline     Frontend Pipeline
              |                   |
              ↓                   ↓
      deploy-backend.sh    deploy-frontend.sh
              |                   |
              ↓                   ↓
          Flask App          Express App
          systemd               PM2
              |                   |
              ↓                   ↓
          Port 5000            Port 3000     



Jenkins Pipeline Configuration

For both Jenkins jobs, I configured:

Pipeline
↓
Pipeline script from SCM
↓
SCM: Git
↓
Repository: GitHub repository
↓
Branch: */main

The Jenkinsfiles are located at:

Backend
backend/Jenkinsfile
Frontend
frontend/Jenkinsfile

This allows Jenkins to obtain the pipeline definition directly from the GitHub repository.



GitHub Webhook

The next step was to automatically trigger Jenkins whenever code was pushed to GitHub.

For this, I configured a GitHub Webhook.

Webhook URL:

http://<EC2-PUBLIC-IP>:8080/github-webhook/

During this project:

http://3.111.36.204:8080/github-webhook/

The webhook was configured for:

Content type: application/json

The event selected was:

Just the push event

The webhook was also set to:

Active





End-to-End CI/CD Test

After configuring the webhook, I performed a real end-to-end test.

A harmless change was made to:

backend/Jenkinsfile

using:

cd ~/flask-express-ec2-jenkins-CI-CD

git status

echo "" >> backend/Jenkinsfile

git add backend/Jenkinsfile

git commit -m "test Jenkins GitHub webhook"

git push origin main

The push successfully triggered Jenkins automatically.





Automatic Pipeline Execution

After the GitHub push, Jenkins automatically started the pipelines.

The following builds were triggered:

Backend-CI-CD  → Build #4
Frontend-CI-CD → Build #3

No manual Build Now action was required after the Git push.

This demonstrated the complete GitHub → Jenkins automation flow.





Backend Build Result

The backend pipeline completed successfully.

Important output included:

Waiting for backend... (1/30)

Backend is ready!

→ Running final health check...

{
  "backend": "Flask Backend",
  "message": "DevOps backend is healthy",
  "status": "Running"
}

========================================
Backend deployment successful!
========================================

Backend CI/CD pipeline completed successfully!

Finished: SUCCESS

Final result:

Backend-CI-CD #4
SUCCESS







Frontend Build Result

The frontend pipeline also completed successfully.

Important output included:

Waiting for Express frontend to become ready...

Frontend is ready!

→ Running final frontend health check...

Frontend health check passed!

========================================
Frontend deployment successful!
========================================

Frontend CI/CD pipeline completed successfully!

Finished: SUCCESS

Final result:

Frontend-CI-CD #3
SUCCESS






Final CI/CD Flow

The final working workflow is:

Developer changes code
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
GitHub
        ↓
GitHub Webhook
        ↓
Jenkins
        ↓
Backend-CI-CD / Frontend-CI-CD
        ↓
Jenkins checks out repository
        ↓
Deployment script
        ↓
Application files synchronized
        ↓
Dependencies installed
        ↓
Application restarted
        ↓
Health check
        ↓
SUCCESS




Backend Deployment Flow
GitHub
   ↓
Jenkins
   ↓
backend/Jenkinsfile
   ↓
deploy-backend.sh
   ↓
rsync
   ↓
Python dependencies
   ↓
systemctl restart backend
   ↓
Flask
   ↓
127.0.0.1:5000
   ↓
Health 



Frontend Deployment Flow
GitHub
   ↓
Jenkins
   ↓
frontend/Jenkinsfile
   ↓
deploy-frontend.sh
   ↓
rsync
   ↓
npm install
   ↓
pm2 restart frontend
   ↓
Express
   ↓
127.0.0.1:3000
   ↓
Health Check




What I Learned From Part 2

Through this part of the project, I learned:

Jenkins

I learned how Jenkins can automate repetitive deployment tasks.

CI/CD

I understood the difference between manually deploying an application and automating the deployment process.

Jenkins Pipelines

I learned how a Jenkinsfile defines the steps Jenkins should execute.

GitHub Webhooks

I learned how GitHub can automatically notify Jenkins when new code is pushed.

Linux Permissions

I learned that Jenkins and application processes can run under different Linux users and that permissions must be handled carefully.

systemd

I learned how Jenkins can restart and verify a systemd-managed application.

PM2

I learned how Jenkins can restart and verify a Node.js application managed by PM2.

Health Checks

I learned that restarting an application and immediately checking it can cause false failures because the application may still be starting.

Retry Logic

Adding a wait/retry mechanism made the deployment pipeline more reliable.
