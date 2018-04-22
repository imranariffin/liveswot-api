def read_from_file(env_var):
	with open('/etc/liveswot-api-env-vars/{}.txt'.format(env_var)) as f:
		ret = f.read().strip()
		if ret == 'True': return True
		if ret == 'False': return False
		return ret
