pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Building the docker image"
                sh "docker build --tag flask_app:2.0 ."
            }
        }
        stage("Run docker images") {
            parallel {
                stage('Run Redis'){
                    steps {
                        echo "Running redis the docker image into container"
                        sh "docker run -d -p 6379:6379 --name redis redis:alpine"
                    }
                }
                stage('Run Flask App'){
                    steps {
                        echo "Running the docker image into container"
                        sh "docker run --detach --publish 5000:5000 --name flask_app_c flask_app:2.0"
                    }
                }
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
                        //sh "python model.py"
                        sh "ab -n 1000 -c 100 http://localhost:5000/"
                        //sh "^C"
                    }
                }
            }
        }
          
        stage("Close") {
            steps {
                echo "Closing the docker containers"
                sh "docker rm -f redis"
                sh "docker rm -f flask_app_c "
                sh "docker rmi -f flask_app:2.0"
            }
        }
    }
}
