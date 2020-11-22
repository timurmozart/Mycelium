mycelium_git="https://github.com/timurmozart/Mycelium"
timestamps{
    node{
        git_pull(mycelium_git)
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