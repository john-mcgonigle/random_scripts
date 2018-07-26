alias ls="ls -G"
alias l='ls -Fhtlr'
alias lsj=' ls -lhra'
alias les=' less -S'
alias add=' git add '
alias st=' git status'
alias co='git co -m '
alias gdev='git co dev'
alias rebase='git pull --rebase'
alias commit=' git commit -m '
alias prev=' git commit --amend'
alias sq=" git commit -m 'squash'"
alias tmn=' tmux new -s '
alias tma=' tmux attach -t '
alias tmls=' tmux ls '
alias tmk=' tmux kill-session -t '
alias szj='du -ha'
alias sztot='du -hs'
alias pyver='python -c '"'"'import sys; print(''"''.''"''.join(map(str, sys.version_info[:3])))'"'"''
alias sapweb='deactivate && source ~/SapWeb/bin/activate && cd ~/sapientia-web && pyver'
alias sapcli='deactivate && source ~/SapClient/bin/activate && cd ~/sapientia-client && pyver'
alias devpy3='deactivate && source ~/DevEnvPy3/bin/activate && pyver'
alias devpy2='deactivate && source ~/BaseDev/bin/activate && pyver'
alias ipy="python -c 'import IPython; IPython.terminal.ipapp.launch_new_instance()'"
alias tree=‘tree -L 2 -C’
alias gl="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset %h' --abbrev-commit --oneline --decorate"
#alias pypath='PYTHONPATH=.:$PYTHONPATH & export PYTHONPATH'
# bsub -J interactive -n 8 -q normal sleep 80000
#the cdmod function chmod sets up a number of sub-functions which in turn allow the user to change to certain directories without wasting much time typing.

 function cdmod()
 {
     function pypath()
     {
        ppath=$(export PYTHONPATH="${PYTHONPATH}:.")
        $ppath
     }
     function cdscr()
     { 
       scripts_dir=$(echo "cd ${HOME}/scripts/")
       $scripts_dir
       ls -lh
     }
     function cddat()
     { 
       exe_dir=$(echo "cd ${HOME}/work_dir/data")
       $exe_dir
       ls -lh
     }

     function cdproj()
     { 
       working_dir=$(echo "cd ${HOME}/Documents/Projects")
       $working_dir
       ls -lh
     }

     function cdst()
     { 
       out_dir=$(echo "cd ${HOME}/working_dir")
       $out_dir
       ls -lh
     }

     function cdtun()
     { 
       seq_dir=$(echo "cd ${HOME}/.ssh")
       $seq_dir
       ls -lh
     }
 }


cdmod
# added by Anaconda3 4.4.0 installer
export PATH="/Users/john.mcgonigle/anaconda/bin:$PATH"
export BCFTOOLS_PLUGINS="/Users/john.mcgonigle/sw/git_libs/bcftools/plugins"
export PATH=$PATH:"/Users/john.mcgonigle/sw/git_libs/bcftools"
export PATH=$PATH:"/Users/john.mcgonigle/sw/git_libs/htslib"
export PATH="/usr/local/sbin:/usr/local/bin:"$PATH

source ~/DevEnvPy3/bin/activate
source ~/.git-completion.bash
[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"
