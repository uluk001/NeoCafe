pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    // Запись информации о последнем коммите
                    sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
                    def lastChanges = readFile('GIT_CHANGES').trim()
                    echo "Last changes: ${lastChanges}"
                }
            }
        }

        stage('Lint and Test') {
            steps {
                script {
                    // Проверка существования директории и её безопасного использования
                    sh 'test -d /home/test/backend || echo "Directory does not exist"'
                    sh '''
                        ssh -v root@164.92.160.185 bash -c "'
                        cd /home/test/backend &&
                        git pull origin main || echo "Не удалось выполнить git pull"
                        '"
                    '''

                    // Построение и запуск контейнеров, выполнение тестов
                    sh 'docker-compose up -d --build'
                    sh 'python3 manage.py test apps'
                    echo "Tests completed"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // SSH и деплой на удаленный сервер
                    sh '''
                        ssh -v root@164.92.160.185 "
                        cd /home/myprojects/backend && 
                        git pull origin main && 
                        docker-compose up -d --build"
                    '''
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
        }
        failure {
            echo "Build failed"
        }
    }
}
