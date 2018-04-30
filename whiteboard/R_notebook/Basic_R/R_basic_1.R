rm(list=ls())
options(encoding = "utf-8")
getwd()
setwd('/Users/john.mcgonigle/Documents/Projects/VP/ortho')

# Assignment
x <- 1
print(x)
x = c(2)
is.vector(x)
print(x)
3 -> x
print(x)

# Vectors
x<-c(1,2,3,4,5,6)
x
x<-1:6
print(typeof(as.integer(x)))
y<-c(1L,2L,3L,4L,5L,6L)
print(typeof(y))
bool<-c(T,F)
print(typeof(bool))
characters<-c('a','b','c')
print(typeof(characters))

# Coercion
# Moves from most to least flexible. 
# Logical < integer < double < character
x<-c(1, 'c', 3)
print(x)
y<-c(T, F, 5)
print(y)
z<-c(1L,2L,3)
print(typeof(z))

# Lists are a little bit mental
x<-list(c(1,2,3), list(c('a','b','c'), c('d','e','f')))
# list of lists containing 3 vectors one numeric, two characters
x
# can view the internals of a list using standard index
x[1]
x[2]

typeof(x)
typeof(x[1])

# However to access the vector contained within need double brackets
x[[2]]
typeof(x[[1]])

typeof(x[[2]][[1]])
typeof(x[[2]][[2]])
x[[2]][[1]][1]

# Factors: - an R class
## Have predefined values (on load) or generation
x <- factor(c("a", "b", "b", "a"))
x
x[2]<-'c'
# Not immutable just won't let you add levels
x
# Attempt to add to a factor without redefining changes the type
print(c(x, 'c'))
# Used to encode categorical variables
typeof(x)
class(x)

# Columns of dataframes are often converted to factors upon loading (will do automatically if they contain a non-numerica character)
## Have to specifically tell it not to!


# Matrix
v<-c(1,2,3,4,5,6)
v
a<-matrix(v, ncol = 3, nrow = 2)
dim(a)
a

# Array 
b <- array(1:12, c(2, 3, 2))
dim(array)

x<-rnorm(100)
y<-rnorm(100)
df<-as.data.frame(cbind(x,y))
dim(df)
str(df)
apply()
aggregrate()