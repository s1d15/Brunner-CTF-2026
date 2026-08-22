module Main where

import Data.Maybe (fromJust)
import Foreign.C.String (CStringLen, peekCAStringLen, castCharToCChar, withCAString)
import Foreign.Marshal.Alloc (mallocBytes, free)
import Foreign.Marshal.Array (pokeArray)
import Text.Read (readMaybe)
import Control.Monad.Trans.Maybe (MaybeT, runMaybeT, hoistMaybe)
import Control.Monad.Trans.Class (lift)
import Control.Monad (mzero)
import System.Exit (exitSuccess)
import System.IO (hSetBuffering, BufferMode(NoBuffering), stdin, stdout, stderr, hSetEncoding, utf8)
import Data.Char (chr, digitToInt)

type Command = [String] -> Notes -> MaybeT IO Notes

type Notes = [(String, CStringLen)]


(!?) :: [a] -> Int -> Maybe a
xs !? n
  | n < 0     = Nothing
  | otherwise = foldr (\x r k -> case k of
                                   0 -> Just x
                                   _ -> r (k-1)) (const Nothing) xs n


fromhex :: String -> Maybe String
fromhex (a:b:rest) = do
  hexrest <- fromhex rest
  return $ chr (16 * digitToInt a + digitToInt b) : hexrest
fromhex [] = Just []
fromhex _ = Nothing

new :: Command
new args notes = do
  name <- hoistMaybe $ args !? 0
  size <- hoistMaybe $ args !? 1 >>= readMaybe
  b <- lift $ mallocBytes size
  lift $ putStrLn $ "Created new note named " ++ name
  return $ (name, (b, size)) : notes


write :: Command
write args notes = do
  name <- hoistMaybe $ args !? 0
  content <- hoistMaybe $ args !? 1
  (string, len) <- hoistMaybe $ lookup name notes
  lift $ pokeArray string (map castCharToCChar $ take len content)
  lift $ putStrLn $ "Wrote content to note " ++ name
  return notes

writehex :: Command
writehex args notes = do
  name <- hoistMaybe $ args !? 0
  content <- hoistMaybe $ args !? 1 >>= fromhex
  (string, len) <- hoistMaybe $ lookup name notes
  lift $ pokeArray string (map castCharToCChar $ take len content)
  lift $ putStrLn $ "Wrote content to note " ++ name
  return notes

view :: Command
view args notes = do
  name <- hoistMaybe $ args !? 0
  cstr <- hoistMaybe $ lookup name notes
  lift $ peekCAStringLen cstr >>= putStrLn
  return notes

delete :: Command
delete args notes = do
  name <- hoistMaybe $ args !? 0
  (b, _) <- hoistMaybe $ lookup name notes
  lift $ free b
  lift $ putStrLn $ "Deleted note " ++ name
  return notes

list :: Command
list _ notes = do
  lift $ putStr (unlines $ map fst notes)
  return notes

commands :: [(String, Command)]
commands = [("new",   new)
           ,("write", write)
           ,("writehex", writehex)
           ,("view",  view)
           ,("delete",  delete)
           ,("exit",  const $ const $ lift $ exitSuccess )
           ,("list", list)]


callCommand :: [String] -> Notes -> MaybeT IO Notes
callCommand (name:args) notes = do
  command <- hoistMaybe $ lookup name commands
  command args notes
callCommand _ _ = mzero

loop :: Notes -> IO ()
loop notes = do
  putStrLn "Commands:"
  putStrLn "  new NAME SIZE"
  putStrLn "  write NAME CONTENT"
  putStrLn "  writehex NAME CONTENT"
  putStrLn "  view NAME"
  putStrLn "  delete NAME"
  putStrLn "  list"
  putStrLn "  exit"

  putStr "> "
  input <- getLine
  result <- runMaybeT $ callCommand (words input) notes
  putStrLn ""
  case result of
    Just notes -> loop notes
    Nothing -> putStrLn "Error running command\n" >> loop notes

main :: IO ()
main = do
  hSetBuffering stdin NoBuffering
  hSetBuffering stdout NoBuffering
  hSetBuffering stderr NoBuffering
  hSetEncoding stdout utf8
  hSetEncoding stderr utf8

  flag <- readFile "flag.txt"
  withCAString flag $ \cstr -> do
        putStrLn "Welcome to my note taking program"
        print cstr
        putStrLn ""
        loop []
