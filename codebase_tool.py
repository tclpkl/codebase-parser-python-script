from helper_classes import codebase_parser
import click

@click.command()
@click.option('-s', '--search_phrase', type=click.STRING, required=True, prompt="Search phrase: ", help="Specifies search phrase to use. ")
@click.option('-b/-a', '--basic/--all-chars', default=True, required=True, help="Specifies whether to perform a basic or all-characters search")
@click.option('-i/-v', '--invisible/--visible', default=True, required=True, help="Specifies whether to run script in background or with a pop-up browser" )
@click.option('-c', '--cluster', default="Bmain (Tempalte)", required=True, help="Specifies which cluster to search (enclose in quotes if whitespace exits). Default set to Bmain (Template) if not specified.")

def search(search_phrase, basic, invisible, cluster):

    # Runs search with parameters from command line (searches through all file types)
    codebase_parser.CodebaseParser.perform_search(search_phrase, {"Select all"}, invisible, basic, cluster)


if __name__ == "__main__":
    search()
