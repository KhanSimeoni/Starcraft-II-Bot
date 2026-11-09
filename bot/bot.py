from sc2.bot_ai import BotAI
from sc2.data import Result

from sc2.ids.unit_typeid import UnitTypeId as uid
from sc2.ids.ability_id import AbilityId as aid
from sc2.ids.upgrade_id import UpgradeId as xid
from sc2.ids.buff_id import BuffId as bid

class CompetitiveBot(BotAI):
    """Main bot class that handles the game logic."""
    
    def __init__(self):
        super().__init__()

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")

        # Remove rally points for manual control of workers
        for townhall in self.townhalls:
            townhall(aid.RALLY_NEXUS, self.start_location)

    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """

        # Keep 70 workers
        if self.workers.amount < 70 and self.can_afford(uid.PROBE):
            for nexus in self.townhalls:
                if nexus.is_idle:
                    nexus.train(uid.PROBE)
                    break

        if self.gas_buildings.amount < 2 * self.townhalls.amount and self.can_afford(uid.ASSIMILATOR):
            for nexus in self.townhalls:
                if self.gas_buildings.closer_than(10, nexus).amount < 2:
                    vgs = self.vespene_geyser.closer_than(10, nexus)
                    for vg in vgs:
                        if self.workers.idle.amount:
                            worker = self.workers.idle.random
                            worker.build(uid.ASSIMILATOR, vg)
                            break
                        else:
                            worker = self.workers.random
                            worker.build(uid.ASSIMILATOR, vg)
                            break
        

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")


    async def on_unit_created(self, unit):
        """
        This code runs whenever a unit is created
        """

        # Worker created logic
        if unit.type_id == uid.PROBE:
            employed = False

            # Join the mines if needed
            for townhall in self.townhalls:
                if townhall.assigned_harvesters < townhall.ideal_harvesters:
                    unit(aid.HARVEST_GATHER, townhall)
                    employed = True
                    break

            # Join the gas if needed and mines are full
            if not employed:
                for assim in self.gas_buildings:
                    if assim.assigned_harvesters < assim.ideal_harvesters:
                        unit(aid.HARVEST_GATHER, assim)
                        employed = True
                        break
            