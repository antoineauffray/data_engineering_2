pipeline
{
    agent any
    stages 
    {
        stage("Build")
        {
            steps
            {
                echo "Building the docker image"
                bash "sudo docker build --tag flask_app:2.0 ."
            }
        }
        stage("Run")
        {
            steps
            {
                echo "Running the docker image into container"
                bash "sudo docker run --detach --publish 5000:5000 --name flask_app_c flask_app:2.0"
            }
        }
        stage("Tests")
        {
            steps
            {
                echo "Running unit test"
                bash "python unittest.py"

                echo "Running integration test"
#                bash "python integration_test.py"
            }
        }
        stage("Close")
        {
            steps
            {
                echo "Closing the docker container"
                bash "sudo docker rm --force flask_app_c"
            }
        }
    }
}
