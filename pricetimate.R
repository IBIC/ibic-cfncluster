library(ggplot2)
library(reshape2)

csv <- read.csv("~/scratch/cfn-estimator/AWS-Estimator/prices.csv", 
                   header=FALSE)

# Assume each bedpostx job takes 411 hours.
time <- 448 
gtime <- time / 14.9

colnames(prices) <- c("instance", "price", "ncpus")

prices <- csv[grep("^[mc]4", csv[, 1]), ]
gprices <- csv[33:34, ]

verticalize <- function(frame, t)
{
  temp <- data.frame(matrix(data=NA, nrow=10^3, ncol=nrow(frame)))
  colnames(temp) <- frame[, 1]
  
  for (col in 1:ncol(temp))
  {
    temp[, col] <- (frame[col, 2] * t * 1:10^3) / frame[col, 3] 
  }
  
  temp$N <- 1:10^3
  
  return(temp)
}

prices.V <- verticalize(prices, time)
prices.V.melt <- melt(prices.V, id.vars="N")
prices.V.melt$class <- ifelse(grepl("^m", prices.V.melt$variable), "Memory",
                              "Compute")


gprices.V <- verticalize(gprices, gtime)
gprices.V.melt <- melt(gprices.V, id.vars="N")
gprices.V.melt$class <- "GPU"

all <- rbind(prices.V.melt, gprices.V.melt)

ggplot(all, aes(x=N, y=value, fill=variable, color=class)) +
  geom_line() + 
  ylim(0, 25000)

