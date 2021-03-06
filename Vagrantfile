Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  
  #redirect traffic from port 5000 on the host machine to port 5000 on the VM
  config.vm.network "forwarded_port", guest: 5000, host: 5000  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
	sudo apt-get update
	sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
	libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
	xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
  
	#uncomment the following line to reprovision with a fresh pyenv installation
	#rm -r ~/.pyenv
	git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  
	#define env variables
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
	echo 'eval "$(pyenv init -)"' >> ~/.profile
	source ~/.profile
  
  
	#install newer python version
	pyenv install 3.8.6
	pyenv global 3.8.6
  
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  

	SHELL
 
  config.trigger.after :up do |trigger|
	trigger.name = "Launching App"
	trigger.info = "Running the TODO app setup script"
	trigger.run_remote = {privileged: false, inline: "
		# Install dependencies and launch
		cd /vagrant
		poetry install
	
		# run flask on 0.0.0.0
		nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
	"}
 end
end
