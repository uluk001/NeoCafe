pipeline {
    agent any

    environment {
        // Определите переменные для использования в пайплайне
        BACKEND_DIR = '/home/test/backend'
        GIT_BRANCH = 'main'
        DEPLOY_SERVER = 'root@164.92.160.185'
        DEPLOY_DIR = '/home/myprojects/backend'
    }

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
                    // Проверка существования директории и прав на неё
                    if (sh(script: "test -d ${BACKEND_DIR}", returnStatus: true) != 0) {
                        error("Directory does not exist: ${BACKEND_DIR}")
                    }

                    // Запуск Redis, Celery и тестов
                    sh """
                        cd ${BACKEND_DIR}
                        git pull origin ${GIT_BRANCH}
                        docker-compose up -d --build
                        python3 manage.py test apps
                    """
                    echo "Redis, Celery started and tests passed"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Передаем переменные и команды в одном блоке sh
                    sh """
                        ssh -v ${DEPLOY_SERVER} << EOF
                        cd ${DEPLOY_DIR}
                        git pull origin ${GIT_BRANCH}
                        docker-compose up -d --build
                        EOF
                    """
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
            // Дополнительные шаги при успешной сборке
        }

        failure {
            echo "Build failed"
            // Дополнительные шаги при неудачной сборке
        }
    }
}
