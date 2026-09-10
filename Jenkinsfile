pipeline {
    agent any

    environment {
        DOCKER_USER = 'shaffat01' // ⚠️ তোমার Docker Hub Username বসাও
        IMAGE_NAME  = 'taskflow-api'
        IMAGE_TAG   = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}" // dev-1, main-2 ইত্যাদি ট্যাগ হবে
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Pulling code from branch: ${env.BRANCH_NAME}"
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                echo "🐳 Building Image for Branch: ${env.BRANCH_NAME}"
                sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                
                echo "🧪 Running Tests..."
                sh "docker run --rm ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} sh -c 'pip install pytest -q && pytest -q'"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh "echo \$DH_PASS | docker login -u \$DH_USER --password-stdin"
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Conditional Deployment') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        echo "🚀 [PRODUCTION DEPLOYMENT] Running on Port 5001..."
                        sh """
                            docker stop taskflow-prod || true
                            docker rm taskflow-prod || true
                            docker run -d --name taskflow-prod -p 5001:5000 ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    } else if (env.BRANCH_NAME == 'dev') {
                        echo "🧪 [DEV DEPLOYMENT] Running on Port 5002..."
                        sh """
                            docker stop taskflow-dev || true
                            docker rm taskflow-dev || true
                            docker run -d --name taskflow-dev -p 5002:5000 ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    } else {
                        echo "ℹ️ Feature branch detected: Skipping deployment."
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo "✅ Branch '${env.BRANCH_NAME}' successfully built and deployed!"
        }
    }
}
