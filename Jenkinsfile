    pipeline{
        agent any
        environment{
            VENV_DIR='../.lama'



        }
        stages{
            stage("cloning Github repo to jenkins"){
                steps{script{
                        echo 'cloning Github repo to Jenkins........'
                        checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token1', url: 'https://github.com/Burak-Akca/Langraph-project.git']])


                }}
            }

                stage("Setting up  our Virtual Enviroment and Installing dependancies"){
                steps{script{
                              sh '''
                    
                
                    python -m venv .venv 
                    
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
             
                    '''

                }}
            }




        }

    }