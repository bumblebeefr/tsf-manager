
Object.defineProperty(Object.prototype, 'getProperty', {
    value: function getProperty(path,default_value){
		var path_array = path.split('.');
		var name = path_array.shift();
		if(name in this){
			if(path_array.length > 0){
				return this[name].getProperty(path_array.join("."),default_value);
			}else{
				return this[name];
			}
		}else{
			return default_value;
		}
	}
});