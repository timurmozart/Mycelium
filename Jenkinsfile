mycelium_git="https://github.com/timurmozart/Mycelium"

properties([
    pipelineTriggers([
        githubPush()
    ])
])

timestamps{
    node{
        git_pull(mycelium_git)
        docker_build()
    }
}

def git_pull(address)
{
    stage("git pull")
    {
        checkout([
            $class: 'GitSCM', 
            branches: [[name: '*/Tymur']], 
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

def docker_build()
{
    stage("Docker build")
    {
        sh '''
            `docker build \
                --rm \
                --tag=mycelium-master:latest \
                ./master/;\
            docker build \
                --rm \
                --tag=mycelium-node:latest \
                ./node/ 
        '''
    }
}