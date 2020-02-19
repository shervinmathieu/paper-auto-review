from textrank import TextRank

"""Access to unified datasets of protein and genetic interactions is critical for interrogation of gene/protein function 
and analysis of global network properties. BioGRID is a freely accessible database of physical and genetic interactions 
available at http://www.thebiogrid.org. BioGRID release version 2.0 includes >116 000 interactions from Saccharomyces cerevisiae, 
Caenorhabditis elegans, Drosophila melanogaster and Homo sapiens. Over 30 000 interactions have recently been added from 5778 sources 
through exhaustive curation of the Saccharomyces cerevisiae primary literature. An internally hyper-linked web interface allows for rapid search 
and retrieval of interaction data. Full or user-defined datasets are freely downloadable as tab-delimited text files and PSI-MI XML. Pre-computed 
graphical layouts of interactions are available in a variety of file formats. User-customized graphs with embedded protein, gene and interaction 
attributes can be constructed with a visualization system called Osprey that is dynamically linked to the BioGRID."""

text = "Access to unified datasets of protein and genetic interactions is critical for interrogation of gene/protein function and analysis of global network properties. BioGRID is a freely accessible database of physical and genetic interactions available at http://www.thebiogrid.org. BioGRID release version 2.0 includes >116 000 interactions from Saccharomyces cerevisiae, Caenorhabditis elegans, Drosophila melanogaster and Homo sapiens. Over 30 000 interactions have recently been added from 5778 sources through exhaustive curation of the Saccharomyces cerevisiae primary literature. An internally hyper-linked web interface allows for rapid search and retrieval of interaction data. Full or user-defined datasets are freely downloadable as tab-delimited text files and PSI-MI XML. Pre-computed graphical layouts of interactions are available in a variety of file formats. User-customized graphs with embedded protein, gene and interaction attributes can be constructed with a visualization system called Osprey that is dynamically linked to the BioGRID."

tr = TextRank()
tr.set_candidate_pos(['NOUN', 'PROPN', 'VERB', 'ADJ'])
tr.analyze(text, window_size=4, lowercase=True)
keywords = tr.get_keywords(10)

print(keywords)