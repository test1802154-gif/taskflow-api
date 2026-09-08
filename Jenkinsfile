pipeline {
    agent any

    environment {
        // ⚠️ নিজের Docker Hub username বসাও
        DOCKER_USER = 'shaffat01'
        IMAGE_NAME  = 'taskflow-api'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        FULL_IMAGE  = "${DOCKER_USER}/${IMAGE_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo "🐳 Building ${FULL_IMAGE}:${IMAGE_TAG}"
                sh """
                    docker build -t ${FULL_IMAGE}:${IMAGE_TAG} .
                    docker tag ${FULL_IMAGE}:${IMAGE_TAG} ${FULL_IMAGE}:latest
                """
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running pytest inside image"
                sh """
                    docker run --rm ${FULL_IMAGE}:${IMAGE_TAG} \
                      sh -c "pip install pytest -q && pytest -q"
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "📤 Login + Push to Docker Hub"
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh """
                        echo "\$DH_PASS" | docker login -u "\$DH_USER" --password-stdin
                        docker push ${FULL_IMAGE}:${IMAGE_TAG}
                        docker push ${FULL_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy from Hub Image') {
            steps {
                echo "🚀 Deploy container on port 5001"
                sh """
                    docker stop taskflow-api || true
                    docker rm taskflow-api || true

                    # Hub থেকে latest pull করে run (production style)
                    docker pull ${FULL_IMAGE}:${IMAGE_TAG}
                    docker run -d --name taskflow-api -p 5001:5000 ${FULL_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Health Check') {
            steps {
                sh """
                    sleep 3
                    curl -sf http://localhost:5001/health
                    echo ""
                    curl -sf http://localhost:5001/ | head -c 200
                    echo ""
                """
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
            sh 'docker image prune -f || true'
        }
        success {
            echo "✅ LIVE: http://SERVER_IP:5001"
            echo "✅ Docker Hub: https://hub.docker.com/r/${DOCKER_USER}/${IMAGE_NAME}"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
