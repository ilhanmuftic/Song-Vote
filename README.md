A bot for a Discord server where musicians gather to collaborate on learning and playing music together. They can suggest songs, vote on which ones they want to learn, confirm their readiness to perform them, and finally access resources like chord sheets to prepare for playing together. The bot acts as a facilitator, guiding this entire process smoothly and automatically, ensuring that all members can participate in an organized way.

Flow and Purpose of Each Channel

**Channel 1**: Song Submissions

This is the starting point for the process. In this channel, any user can chat freely, but the primary purpose is for users to submit songs they think the group should learn. They do this by typing a command along with a link to the song (e.g., a YouTube URL). The bot detects this command and automatically moves the song suggestion to the next channel for voting. This keeps the conversation clean and focused, allowing only approved songs to move forward.

**Channel 2**: Voting on Songs

In this channel, users cannot send messages, but they can react to messages that the bot posts. This is where the group votes on which songs they want to learn. For every song submitted in Channel 1, the bot creates a message here, and users can vote by reacting (e.g., giving a thumbs up). When all users have voted or a set number of positive votes is reached, the bot automatically moves the song to the next channel, signaling that it has been approved by the community.

**Channel 3**: Confirming Readiness to Play

After a song is voted on and approved, it appears in this channel. Similar to the previous channel, users cannot send messages here, but they can react to indicate their readiness. The idea is that after learning and practicing the song, each musician can confirm they are ready to play it by reacting with a specific emoji (like a checkmark). Once all participants have confirmed, the bot moves the song to the final channel.

**Channel 4**: Songs Ready to Play with Chords

This is the final stage for each song. Only admins can post in this channel, but everyone can view it. When a song reaches this point, it means the group is ready to play it together. Admins can reply to the song message with an image that contains the chords or sheet music needed for the song. This way, all the songs that the group is prepared to play are listed in one place, with easy access to the resources needed to perform them.
