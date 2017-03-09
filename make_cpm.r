library(ggplot2)
library(reshape2)
library(plyr)
library(scales)


# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


setwd_thisdir <- function () {
  this.dir <- dirname(parent.frame(3)$ofile)
  setwd(this.dir)
}

tbl <- read.table("input_R.csv",header=TRUE,sep =",", fill = TRUE)


output_eps <- "CPM.eps"
text_font <- 20
point_font <- 2
line_font <- .3



tbl$contigs2 <- factor(tbl$n2, levels = tbl$ordering)
tbl$contigs1 <- factor(tbl$n1, levels = tbl$ordering)
tbl$ordered <- factor(tbl$ordering,levels=unique(tbl$ordering))

p1<-ggplot(data=subset(tbl, !is.na(ordered)), aes(x = ordered, y = log10(nlength))) +
  geom_line(group = 1) +
  labs(x="Contigs",y=expression(~log[10]~(length))) +
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  theme(axis.line.x = element_line(color="black", size = 0.5),
        axis.line.y = element_line(color="black", size = 0.5),
        axis.title.x = element_text(size = text_font-3, angle = 0),
        axis.title.y = element_text(size = text_font-3, angle = 90),
        legend.title=element_text(size= text_font-3),
        legend.text=element_text(size = text_font-3),
        plot.margin=unit(c(0,0.03,0.5,0),units="npc")
  )


p2<-ggplot(data=subset(tbl, !is.na(ordered)), aes(x = ordered, y = log10(coverage))) +
  geom_line(group = 1) +
  labs(x="Contigs",y=expression(~log[10]~(Coverage))) +
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  theme(axis.line.x = element_line(color="black", size = 0.5),
        axis.line.y = element_line(color="black", size = 0.5),
        axis.title.x = element_text(size = text_font-3, angle = 0),
        axis.title.y = element_text(size = text_font-3, angle = 90),
        legend.title=element_text(size= text_font-3),
        legend.text=element_text(size = text_font-3), 
        plot.margin=unit(c(-0.5,0.03,1,0),units="npc")
  )
p2


p3 <- ggplot(tbl, aes(contigs1, contigs2)) + 
  geom_tile(aes(fill = log10(nlinks)), colour = "white", size=0.001) + 
  scale_fill_gradient(low = "burlywood1", high = "#FF0000", space = "Lab", na.value = "grey50", 
                      guide = "colourbar") + 
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank()) +
  labs(x="Contigs",y="Contigs") +
  theme(axis.line.x = element_line(color="black", size = 0.5),
        axis.line.y = element_line(color="black", size = 0.5),
        axis.title.x = element_text(size = text_font-3, angle = 0),
        axis.title.y = element_text(size = text_font-3, angle = 90),
        legend.title=element_text(size= text_font-3),
        legend.text=element_text(size = text_font-3))+
        guides(fill = guide_legend(keywidth = 1, keyheight = 3,
                                   title = expression(~log[10]~(nlinks)))) 


cairo_ps(output_eps, width = 14, height = 20)
multiplot(p3, p1, p2, cols=1)
dev.off()

