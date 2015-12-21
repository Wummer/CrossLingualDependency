# CrossLingualDependency

=======================
*HOW TO:*

1. Acquire "Universal Dependencies v1.1" and "SPMRL" data sets.
2. Run convert_all_data.py with either UD or SPMRL as argument
3. Optional: run run_dev.py to run the dev experiments (must change settings in file)
4. Run run_thesis.py with UD or SPMRL as argument. See file for different settings.
5. ?????
6. Profit

If you use SPMRL dataset, remember to use the mapping.py to map the language specific pos tags to the universal tags.


----------------------
Notes on 3rd party software:

As I don't host any of the used data sets or the parser itself, you can find links below:


* Universal Dependencies v1.1 : https://universaldependencies.github.io/docs/
* Hanstholm parser: https://github.com/andersjo/hanstholm
* Retrofitting (is already included, but for good measure): https://github.com/mfaruqui/retrofitting 


SPMRL is not available to the public hence there is no link, sorry.

