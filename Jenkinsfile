repo="https://github.com/timurmozart/Mycelium"
branch="*/Tymur"

properties([
    pipelineTriggers([
        githubPush()
    ])
])

timestamps{
    node{
        docker_kill()
        git_pull(repo, branch)
        docker_compose_build()
        docker_run()
        docker_test()
        docker_kill()
    }
}

def git_pull(repo, branch){
    stage("git pull")
    {
        checkout([
            $class: 'GitSCM', 
            branches: [[name: branch]], 
            doGenerateSubmoduleConfigurations: false, 
            extensions: [], 
            submoduleCfg: [], 
            userRemoteConfigs: [[
                credentialsId: 'github', 
                url: 'https://github.com/timurmozart/Mycelium'
            ]]
        ])
    }
}

def docker_build(){
    stage("Docker build")
    {
        sh '''
            docker build \
                --rm \
                --tag=mycelium-master:latest \
                ./master/
            docker build \
                --rm \
                --tag=mycelium-node:latest \
                ./node/ 
        '''
    }
}

def docker_run(){
    stage("Docker run")
    {
        sh '''
            docker run \
                -itd \
                --rm \
                --hostname=myc-n \
                -p 8000/tcp \
                --name myc-n1 \
                --network=myc \
                mycelium-node:latest
            docker run \
                -itd \
                --rm \
                --hostname=myc-n \
                -p 8000/tcp \
                --name myc-n2 \
                --network=myc \
                mycelium-node:latest
            docker run \
                -itd \
                --rm \
                -p 5000:5000 \
                --name myc-m \
                --hostname=myc-m \
                --network=myc \
                mycelium-master:latest
        '''
    }
}

def docker_kill(){
    stage("kill containers")
    {
        sh '''
            docker kill myc-n myc-m myc-s || echo "nothing to stop"
        '''
    }
}

def docker_test(){
    stage("test"){
        sh '''
            docker build \
                --rm \
                --tag=mycelium-sender:latest \
                ./sender/
        '''
        sh '''
            docker run \
                -t \
                --rm \
                --hostname=myc-s \
                --name myc-s \
                --network=myc \
                mycelium-sender:latest
        '''

        // sh 'ls -lh /usr/bin/'
        
        // sh 'cat ./sender/main.py'
        // sh 'python -m pip install requests'
        // sh '/usr/bin/python ./sender/main.py'
        
    }
}

def docker_compose_build(){
    stage('docker-compose build') {
        sh "ls -la"
        sh "docker-compose build"
    }
}