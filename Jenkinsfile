repo="https://github.com/timurmozart/Mycelium"
branch="*/Tymur"

properties([
    pipelineTriggers([
        githubPush()
    ])
])

timestamps{
    node{
        git_pull(mycelium_git)
        docker_build()
        docker_run()
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
                --name myc-n \
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

def docker_stop(){
    stage("stop containers")
    {
        sh '''
            docker kill myc-n myc-m
        '''
    }
}

