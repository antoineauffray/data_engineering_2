pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Building the docker image"
                sh "docker build --tag flask_app:2.0 ."
            }
        }
        stage("Run docker images: Flask App") {
            steps {
                echo "Running the docker image into container"                    
                sh "docker run --detach --publish 5000:5000 --name flask_app_c flask_app:2.0"
            }
        }

        stage("Tests") {
            parallel {
                stage('Test Unit test'){
                    steps { 
                        echo "Running unit test"
                        sh "python unittest_model.py"
                    }  
                }
                stage('Test Integration test'){
                    steps {
                        echo "Running integration test"
                        sh "python integration_test.py"
                    }
                }
                stage('Test stress test'){
                    steps {
                        echo "Running stress test"
                        sh "ab -n 1000 -c 100 http://localhost:5000/"
                    }
                }
            }
        }
          
        stage("Close") {
            steps {
                echo "Closing the docker containers"
                sh "docker rm -f flask_app_c "
                sh "docker rmi -f flask_app:2.0"
            }
        }

        stage('Release'){
            when{ 
                expression {
                    env.BRANCH_NAME == 'development'}
            }
            steps{
                sh 'git branch -d release'
                sh 'git checkout -b release'
                sh 'git pull –rebase'
                sh 'git push origin release'
            }
        }
        
        stage('Validation Test'){
            when{ 
                expression {
                    env.BRANCH_NAME == 'release'}
            }
            steps{
                echo 'automatic merging not permitted'
            }
        }
    }
}
