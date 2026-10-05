pipeline {
    agent any

    environment {
        IMAGE_NAME = 'studyhub'
        VENV       = '.venv'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') { steps { checkout scm } }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps { sh '. ${VENV}/bin/activate && flake8 app tests wsgi.py --max-line-length=100' }
        }

        stage('Test') {
            steps {
                sh '. ${VENV}/bin/activate && pytest --junitxml=test-results.xml --cov=app --cov-report=xml'
            }
            post { always { junit 'test-results.xml' } }
        }

        stage('Build Docker Image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .' }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ${IMAGE_NAME} || true
                    docker run -d --name ${IMAGE_NAME} -p 5000:5000 \
                        -v studyhub-data:/app/instance ${IMAGE_NAME}:latest
                    sleep 4
                    curl -f -o /dev/null http://localhost:5000/login
                '''
            }
        }
    }

    post {
        success { echo 'StudyHub deployed at http://<jenkins-host>:5000' }
        failure { echo 'Pipeline failed - check the stage logs.' }
    }
}
