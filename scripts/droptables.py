from authenticationjwt.models import User
from swot.models import Swot
from swot_item.models import SwotItem
from swot_item_vote.models import Vote
from swot_members.models import SwotMember, Invite


print 'deleting all rows in all tables ...'
Invite.objects.all().delete()
SwotMember.objects.all().delete()
Vote.objects.all().delete()
SwotItem.objects.all().delete()
Swot.objects.all().delete()
User.objects.all().delete()
print 'Done deleting rows in tables Invite, SwotMember, Vote, SwotItem, Swot, User'
