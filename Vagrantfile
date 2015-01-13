# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define :findaconf do |findaconf|
  
	findaconf.vm.box = "ubuntu/trusty32"
	findaconf.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty32"
	
	findaconf.vm.provider :parallels do |parallels, override|
		override.vm.box = "parallels/ubuntu-14.04"
		override.vm.box_url = "https://vagrantcloud.com/parallels/boxes/ubuntu-14.04"
		parallels.update_guest_tools = true
    	parallels.optimize_power_consumption = false
   		parallels.memory = 1024
	end

	findaconf.vm.provision :shell, path: "Vagrant.sh"
	findaconf.vm.network :forwarded_port, host: 5000, guest: 5000

  end
end
