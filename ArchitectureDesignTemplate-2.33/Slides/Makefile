MAIN := dsnSlidesArchitectureTemplates
TEX := $(MAIN).tex
PDF := $(MAIN).pdf
INSTRUCTOR_TEX := $(MAIN)Instructor.tex
INSTRUCTOR_PDF := $(MAIN)Instructor.pdf
CHAPTER_TIKZ := ../TikZ/dsnIntroduction/dsnVModel.tex ../TikZ/dsnIntroduction/dsnMaintainedSourceComparison.tex ../TikZ/dsnIntroduction/dsnArchitectureUpdateFeedback.tex

.PHONY: all instructor clean
all: $(PDF)
$(PDF): $(TEX) beamerThemeSlides.sty dsnTemplateVersion.tex $(wildcard slides/*.tex) $(wildcard assets/*) $(CHAPTER_TIKZ)
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(TEX)
instructor: $(INSTRUCTOR_PDF)
$(INSTRUCTOR_PDF): $(INSTRUCTOR_TEX) $(TEX) beamerThemeSlides.sty dsnTemplateVersion.tex $(wildcard slides/*.tex) $(wildcard assets/*) $(CHAPTER_TIKZ)
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(INSTRUCTOR_TEX)
clean:
	latexmk -C $(TEX)
	latexmk -C $(INSTRUCTOR_TEX)
