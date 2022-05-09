from Chromosome import Chromosome
class ChromosomeCopy:
      def copy(chromosome:Chromosome):
        copy=Chromosome()
        assert isinstance(chromosome,Chromosome)
        for section in chromosome.getSections():
            copy_section=copy.createSection()
            for unit in section.getUnits():
                copy_unit=copy_section.createUnit()
                for task in unit.getTasks():
                    copy_unit.setTask(task)
        return copy

