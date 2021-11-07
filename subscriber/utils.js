export function processMessage(buf) {
	let json;
	if (buf.length > 30) { return null; }	
	try {
		json = JSON.parse(buf.toString('ascii'))	
	} catch (e) {
		return null;
	}
	if (!('temp' in json)) { return null; }
	if (!('hum' in json)) { return null; }
	return json
}

