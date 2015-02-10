/**
 * Serialize form fields into JSON
 */

(function($) {
	function escapeStr(str) {
		if (str)
			return str.replace(/([ #;?%&,.+*~\':"!^$[\]()=>|\/@])/g, '\\$1');

		return str;
	}
	;
	$.fn.serializeJSON = function() {
		var json = {};
		var form = $(this);
		form.find('input, select').each(function() {
			var val;
			if (!this.name)
				return;

			if ('radio' === this.type) {
				if (json[this.name]) {
					return;
				}

				json[this.name] = this.checked ? this.value : '';
			} else if ('checkbox' === this.type) {
				val = json[this.name];
				if (!this.checked) {
					if (!val) {
						json[this.name] = '';
					}
				} else {
					json[this.name] = typeof val === 'string' ? [ val, this.value ] : $.isArray(val) ? $.merge(val, [ this.value ]) : this.value;
				}
			} else {
				json[this.name] = this.value;
			}
		});
		return json;
	};
	$.fn.deserializeJSON = function(json, clear_unknown) {
		if (json == null)
			json = {};
		var form = $(this);

		form.find("input,textarea,select").each(function() {
			var self = $(this);
			if (self.is("input[type=radio],input[type=checkbox]")) {
				if (json[self.attr('name')] == self.val()) {
					self.prop('checked', true);
				} else {
					self.prop('checked', false);
				}
			} else {
				if (self.attr('name') in json) {
					self.val(json[self.attr('name')]);
				} else {
					if (clear_unknown) {
						self.val('');
					}
				}
			};
		});
	};
})(jQuery);