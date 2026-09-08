pipeline {
    agent any

    environment {
        IMAGE_NAME = "taskflow-api"
        // Docker Hub username — নিজেরটা বসাও (optional push এর জন্য)
        DOCKER_USER = "shaffat01"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Run Tests in Container') {
            steps {
                sh """
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} \
                      sh -c "pip install pytest -q && pytest -q"
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker stop taskflow-api || true
                    docker rm taskflow-api || true
                    docker run -d --name taskflow-api -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Health Check') {
            steps {
                sh """
                    sleep 3
                    curl -sf http://localhost:5001/health
                    curl -sf http://localhost:5001/tasks
                """
            }
        }
    }

    post {
        success {
            echo "✅ TaskFlow API LIVE on port 5001"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
