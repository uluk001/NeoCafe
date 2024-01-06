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
                    echo "Deployment successful"
                }
            }
        }

        stage('Publish results') {
            steps {
                script {
                    // Публикация результатов тестов
                    echo "Publishing results"
                }
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
