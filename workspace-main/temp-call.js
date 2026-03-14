const { Core } = require('@larksuiteoapi/node-sdk');

// Create a client
const client = new Core({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET,
});

// Make an audio call
async function makeCall(userId) {
  try {
    const response = await client.post('im', 'v1/calls/audios', {
      user_id: userId,
    }, {
      params: { receive_id_type: 'user_id' }
    });
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Get user ID from command line
const userId = process.argv[2];
if (!userId) {
  console.log('Usage: node temp-call.js <user_id>');
  process.exit(1);
}

makeCall(userId);
