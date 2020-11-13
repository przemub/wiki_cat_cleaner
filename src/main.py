import gettext
import sys
from typing import List

from pywikibot import Category, Site, Page
from pywikibot.pagegenerators import CategorizedPageGenerator

trans = gettext.translation('base', localedir='locales')
_ = trans.gettext


def clean(category: Category, supercategories: List[Category]):
    print(_("Cleaning category {0}").format(category.title()))
    for page in CategorizedPageGenerator(category):
        page: Page

        for page_category in page.categories():
            if page_category in supercategories:
                print(_("{0}: Removing {1}, a supercategory of {2}").format(
                    page.title(), page_category.title(), category.title()
                ))
                page.change_category(
                    page_category,
                    None,
                    _("Removed {0} since it is a supercategory of {1}").format(
                        f"[[{page_category.title()}]]",
                        f"[[{category.title()}]]"
                    )
                )

    for subcategory in category.subcategories():
        clean(subcategory, supercategories + [category])


def main():
    site = Site()

    if len(sys.argv) < 2:
        category_name = input(_("Category to clear: "))
    else:
        category_name = sys.argv[1]

    category = Category(site, category_name)
    clean(category, [])


if __name__ == '__main__':
    main()
