pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = env.DOCKER_REGISTRY ?: ''
        IMAGE_TAG = env.BUILD_NUMBER ? "${env.BUILD_NUMBER}" : "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Backend') {
            steps {
                dir('backend') {
                    // Assuming Node.js/npm or python or maven backend. Let's check common patterns or execute npm test / pytest if available.
                    // We will run standard npm test if package.json exists, or fallback/conditional.
                    sh 'if [ -f package.json ]; then npm install && npm test; elif [ -f requirements.txt ]; then pip install -r requirements.txt && pytest; fi'
                }
            }
        }

        stage('Test Frontend') {
            steps {
                dir('frontend') {
                    sh 'if [ -f package.json ]; then npm install && npm test -- --watchAll=false; fi'
                }
            }
        }

        stage('Build Docker Images') {
            parallel {
                stage('Build Frontend Image') {
                    steps {
                        script {
                            def frontendContext = fileExists('frontend/Dockerfile') ? 'frontend' : '.'
                            def dockerfile = fileExists('frontend/Dockerfile') ? 'frontend/Dockerfile' : 'Dockerfile.frontend'
                            sh "docker build -t frontend:${IMAGE_TAG} -f ${dockerfile} ${frontendContext}"
                        }
                    }
                }
                stage('Build Backend Image') {
                    steps {
                        script {
                            def backendContext = fileExists('backend/Dockerfile') ? 'backend' : '.'
                            def dockerfile = fileExists('backend/Dockerfile') ? 'backend/Dockerfile' : 'Dockerfile.backend'
                            sh "docker build -t backend:${IMAGE_TAG} -f ${dockerfile} ${backendContext}"
                        }
                    }
                }
                stage('Build Nginx Image') {
                    steps {
                        script {
                            def nginxContext = fileExists('nginx/Dockerfile') ? 'nginx' : '.'
                            def dockerfile = fileExists('nginx/Dockerfile') ? 'nginx/Dockerfile' : 'Dockerfile.nginx'
                            sh "docker build -t nginx:${IMAGE_TAG} -f ${dockerfile} ${nginxContext}"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
