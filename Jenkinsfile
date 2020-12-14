pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Building the docker image"
                sh "sudo docker build --tag flask_app:2.0 ."
            }
        }
        stage("Run") {
            steps {
                echo "Running the docker image into container"
                sh "sudo docker run --detach --publish 5000:5000 --name flask_app_c flask_app:2.0"
            }
        }
        stage("Tests") {
            steps {
                echo "Running unit test"
                sh "python unittest.py"

                echo "Running integration test"
//                bash "python integration_test.py"
            }
        }
        stage("Close") {
            steps {
                echo "Closing the docker container"
                sh "sudo docker rm --force flask_app_c"
            }
        }
    }
}
