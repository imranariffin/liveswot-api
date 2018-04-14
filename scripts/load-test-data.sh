#!bin/sh
# dependency: `npm install -g nodemon`

SPACE=' '
USER_FIXTURES=authenticationjwt/fixtures/users.json
SWOT_FIXTURES=swot/fixtures/swots.json
ITEM_FIXTURES=swot_item/fixtures/swotItems.json
VOTE_FIXTURES=swot_item_vote/fixtures/votes.json

FIXTURES="$USER_FIXTURES${SPACE}$SWOT_FIXTURES"
FIXTURES="$FIXTURES${SPACE}$ITEM_FIXTURES${SPACE}$VOTE_FIXTURES"

cd $HOME/liveswot-api
python manage.py loaddata $FIXTURES