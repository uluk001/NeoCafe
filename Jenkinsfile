pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm

                script {
                    sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
                    def lastChanges = readFile('GIT_CHANGES')
                    echo "Last changes: ${lastChanges}"
                }
            }
        }

    stage('Lint and Test') {
        steps {
            script {
                // Запуск Redis и Celery
                sh 'docker run -d --name redis redis'
                sh 'celery -A your_project_name worker --loglevel=info &'

                // Запуск линтеров
                sh 'flake8 .'
                sh 'black --check .'

                // Запуск тестов
                sh 'python3 manage.py test apps'
            }
        }
    }

    stage('Deploy') {
        steps {
            script {
                sh 'ssh -v root@164.92.160.185 "cd /home/myprojects/backend && git pull origin main && docker-compose up -d --build"'
            }
        }
    }

        stage('Publish results') {
            steps {
                echo "Deployment successful"
            }
        }
    }

    post {
        success {
            echo "Build successful"
            // You can add additional steps here, like running tests or notifications.
        }

        failure {
            echo "Build failed"
        }
    }
}
