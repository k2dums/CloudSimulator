from Chromosome import Chromosome
class ChromosomeCopy:
    """
    Class is used to copy a chromsome instance and return that copied instance\n
    """
    def copy(chromosome:Chromosome):
        """Copies the Chromosome instance and returns another copied instance of the Chromosome instance"""
        copy=Chromosome()
        assert isinstance(chromosome,Chromosome)
        for section in chromosome.getSections():
            copy_section=copy.createSection()
            for unit in section.getUnits():
                copy_unit=copy_section.createUnit()
                for task in unit.getTasks():
                    copy_unit.setTask(task)
        return copy

