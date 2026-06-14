pipeline {
    agent any
    triggers {
        GenericTrigger(token: 'CI_TRIGGER_A87B89')
    }
    environment {
        DOCKERHUB_USER = 'mubashirhassan'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        APP_CONTAINER = 'sentiment-app-ci'
        BASE_URL = 'http://localhost:5000'
    }
    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }
        stage('Build and Run') {
            steps {
                sh 'docker stop ${APP_CONTAINER} || true'
                sh 'docker rm ${APP_CONTAINER} || true'
                sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:unstable .'
                sh 'mkdir -p /tmp/app-logs'
                sh 'docker run -d --name ${APP_CONTAINER} -p 5000:5000 -v /tmp/app-logs:/app/logs ${DOCKERHUB_USER}/sentiment-api:unstable'
                sh 'sleep 45'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'docker run --rm --network host -e BASE_URL=${BASE_URL} ${DOCKERHUB_USER}/sentiment-api:unstable python -m pytest tests/test_api.py -v'
            }
        }
        stage('UI Test') {
            steps {
                sh 'BASE_URL=${BASE_URL} python3 -m pytest tests/test_ui.py -v'
            }
        }
        stage('Build and Push') {
            steps {
                sh 'echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin'
                sh 'docker push ${DOCKERHUB_USER}/sentiment-api:unstable'
                sh 'git fetch --all'
                sh 'git show origin/stable-fallback:app.py > /tmp/stable_app.py'
                sh 'cp app.py /tmp/main_app.py && cp /tmp/stable_app.py app.py'
                sh 'docker build -t ${DOCKERHUB_USER}/sentiment-api:stable .'
                sh 'cp /tmp/main_app.py app.py'
                sh 'docker push ${DOCKERHUB_USER}/sentiment-api:stable'
                sh 'docker logout'
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f k8s/pvc.yaml'
                sh 'kubectl apply -f k8s/blue-deployment.yaml'
                sh 'kubectl apply -f k8s/green-deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/sentiment-blue-deployment --timeout=180s'
            }
        }
    }
    post {
        always {
            sh 'docker stop ${APP_CONTAINER} || true'
            sh 'docker rm ${APP_CONTAINER} || true'
        }
    }
}
