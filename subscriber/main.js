#!/usr/local/bin/node

import dgram from 'dgram'
import fs from 'fs'
import { processMessage } from './utils.js'

const port = 24121
const file = 'log.json'

const server = dgram.createSocket('udp4')

server.on('error', (err) => {
	console.error("Error starting server: " + err)
})

server.on('message', (buf, rinfo) => {
	const json = processMessage(buf)
	if (json == null) {
		// There was loss, corruption or unwanted traffic
		console.error(
			"Invalid message: " + buf.toString() + '\n'
			+ "IP: " + rinfo.address + '\n'
		)
		return;
	}
	json.timestamp = new Date().getTime()
	fs.appendFile(file, JSON.stringify(json) + '\n', { encoding: 'ascii' }, (err) => {
		return err && console.error("Error while appending data to file: " + err)
	})
})

server.on('listening', () => {
	const address = server.address()
	console.log(`server listening ${address.address}:${address.port}`)
})

server.bind(port)
