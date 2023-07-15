# Oreo

## Why is it called Oreo? Thats not a Vegi
> yoeyshapiro: Someone name a vegetable<br>
> BRIN: Good, that's the plan. The promo bot exists as a cattle prod for your ass<br>
> ponyboi: Oreos<br>
> BRIN: Squash<br>
> yoeyshapiro:<br>
>     I'm gonna try to let people give custom messages<br>
>     Squash is taken<br>
>     Is oero a vegi<br>
> ponyboi: Yes<br>

discord bot to deal with adding new stuff
done by users
can make custom messages with variables
cant just have webhook, need bot to
maybe use both, at first

add the discord server to bot and db. how does webhook handle it.
needs its own hook. so hook is in db too

so maybe have bot send message, but later

will need to be bot to maybe delete messages
make another table for server/channels
channel name and stuff cannot be unique, multiple servers might request that channel

maybe one call for everything, we will see. but twitch needs it this way
should use different functions, more organized, but break up and share what i can
because each one has its own way of forming links. just try

https://dev.twitch.tv/docs/cli/event-command/
https://dev.twitch.tv/docs/api/reference/

and need a bot for custom messages

add "subscription system

ADD files to docker when im done. more standard, shouldnt need to modify, give image only or something. at least stick
have dockeer file on docker hub. they dont need src anymore
https://letsencrypt.org/

maybe get steam info from discord, how does pingbot do it.
ill just do it my own way

[twitch sub types](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#subscription-types)
[manage subs](https://dev.twitch.tv/docs/eventsub/manage-subscriptions/)

should close port, but dont need to. later close and use docker port
