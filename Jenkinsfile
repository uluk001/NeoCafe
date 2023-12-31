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

        stage('Test') {
            steps {
                script {
                    // SSH и деплой на удаленный сервер
                    sh '''
                        ssh -v root@164.92.160.185 "
                        cd /home/test/backend &&
                        git pull origin main &&
                        docker-compose up -d --build
                        docker exec -it backend python3 manage.py test apps"
                    '''
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
