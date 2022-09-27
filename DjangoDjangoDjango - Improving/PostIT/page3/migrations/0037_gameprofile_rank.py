# Generated by Django 3.2.15 on 2022-09-27 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page3', '0036_gameprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameprofile',
            name='rank',
            field=models.CharField(choices=[('Val', [('IRON', 'Iron :((('), ('Bronze', 'Bronze :(('), ('Silver', 'Silver :('), ('Gold', 'Gold :('), ('Platinum', 'Platinum '), ('Diamond', 'Diamond :) '), ('Asencdant', 'Asencdant :)) '), ('Immortal', 'Immortal >_< '), ('Radiant', 'Radiant :> ')]), ('COD', [('Rookie', 'Rookie :((('), ('Veteran', 'Veteran :(('), ('Elite', 'Elite :('), ('Pro', 'Pro :('), ('Master', 'Master '), ('Grandmaster', 'Grandmaster :) '), ('Legendary', 'Legendary :)) ')]), ('LOL', [('IRON', 'Iron :((('), ('Bronze', 'Bronze :(('), ('Silver', 'Silver :('), ('Gold', 'Gold :('), ('Platinum', 'Platinum '), ('Diamond', 'Diamond :) '), ('Master', 'Master :)) '), ('Grandmaster', 'Grandmaster >_< '), ('Challenger', 'Challenger :> ')]), ('CS', [('Silver', 'Silver :('), ('Gold', 'Gold :('), ('Master Guardian', 'Master Guardian '), ('Distinguished Master Guardian', 'Distinguished Master Guardian :) '), ('Legendary', 'Legendary :)) '), ('Elite', 'Elite >_< ')])], default='', max_length=50),
        ),
    ]